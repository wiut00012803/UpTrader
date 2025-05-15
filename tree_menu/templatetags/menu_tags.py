from django import template
from django.urls import reverse
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    items = list(
        MenuItem.objects
        .filter(menu__name=menu_name)
        .order_by('sort_order')
    )

    id_map = {i.id: i for i in items}
    children = {}
    for i in items:
        children.setdefault(i.parent_id, []).append(i)

    for i in items:
        if i.named_url:
            url = reverse(i.named_url)
        else:
            url = i.url or ''
        if not url.startswith(('/', 'http://', 'https://')):
            url = '/' + url.lstrip('/')
        i.resolved_url = url

    current = next((i for i in items if i.resolved_url == request.path), None)
    active_ids = set()
    current_id = None
    if current:
        current_id = current.id
        node = current
        while node:
            active_ids.add(node.id)
            node = id_map.get(node.parent_id)

    def build(parent_id):
        result = []
        for item in children.get(parent_id, []):
            if parent_id is None or item.id in active_ids:
                result.append({
                    'item': item,
                    'children': build(item.id)
                })
        return result

    tree = build(None)

    return {
        'nodes': tree,
        'active_ids': active_ids,
        'current_id': current_id,
        'request': request,
    }
