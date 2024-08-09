from django import template
from menu.models import MenuItem
from django.utils.safestring import mark_safe

register = template.Library()


def build_menu_tree(menu_items):
    tree = {}
    items_dict = {item.id: item for item in menu_items}
    children_dict = {}

    for item in menu_items:
        parent_id = item.parent_id
        item.children = []
        if parent_id:
            if parent_id not in children_dict:
                children_dict[parent_id] = []
            children_dict[parent_id].append(item)
        else:
            if item.menu_name not in tree:
                tree[item.menu_name] = []
            tree[item.menu_name].append(item)

    for parent_id, children in children_dict.items():
        parent = items_dict[parent_id]
        parent.children.extend(children)

    return tree


def render_menu(items, active_item):
    def is_active(item):
        return item == active_item or any(is_active(child) for child in item.children)

    output = '<ul>'
    for item in items:
        active_class = 'class="active"' if is_active(item) else ''
        output += f'<li {active_class}><a href="{item.get_url()}">{item.name}</a>'
        if item.children:
            output += render_menu(item.children, active_item)
        output += '</li>'
    output += '</ul>'
    return output


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')
    active_item = None
    for item in menu_items:
        if item.get_url() == current_url:
            active_item = item
            break

    tree = build_menu_tree(menu_items)
    menu_html = render_menu(tree.get(menu_name, []), active_item)
    return mark_safe(menu_html)