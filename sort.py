"""Sorts password"""

def main():
    "Main Program"
    file = input('Name the password file. Default: Bitwarden_Pswds.csv') or 'Bitwarden_Pswds.csv'
    with open(file, 'r', encoding='utf-8') as pswds:
        with open('Sorted_Pswds.csv', 'w', encoding='utf-8') as sort:
            categories = pswds.readline().split(',')

            print('Which category to sort? (Case sensitive)')
            print('For hierarchical sorting, separate categories with commas (e.g., "name,folder")')
            print('Available categories:', ', '.join(categories))
            print('Note: Some fields may not be useful to sort.')
            select = input('  > ')

            # Handle multiple categories
            selected_cats = [cat.strip() for cat in select.split(',')]
            idx = []
            for cat in selected_cats:
                if cat not in categories:
                    print(f'Category "{cat}" does not exist.')
                    return
                idx.append(categories.index(cat))

            passwords = list(map(format_pswd, pswds))

            passwords = sort_it(passwords, idx)

            sort.write(','.join(categories))
            for line in passwords:
                sort.write(','.join(line) + '\n')

def format_pswd(item:str):
    """Strip it and segment each"""
    strip = item.rstrip()
    return strip.split(',')

def compare_items(item1, item2, cat_indices):
    """Compare two items based on hierarchical category indices.
    Returns: -1 if item1 < item2, 0 if equal, 1 if item1 > item2"""
    for cat in cat_indices:
        val1, val2 = item1[cat], item2[cat]
        if val1 < val2:
            return -1
        elif val1 > val2:
            return 1
    return 0  # All categories are equal

def sort_it(items, cat):
    """Sorts passwords based on selected categories (hierarchical)"""

    new_items = [items[0]]

    for i in items[1:]:
        l, r = 0, len(new_items)
        print(f"Inserting: {i}")
        while l < r:
            mid = (l + r) // 2
            comparison = compare_items(i, new_items[mid], cat)

            # Debug output showing hierarchical comparison
            cat_values = [f"'{i[c]}' vs '{new_items[mid][c]}'" for c in cat]
            print(f"  l={l}, mid={mid}, r={r}, comparing {cat_values}, result={comparison}")

            if comparison > 0:  # i > new_items[mid]
                l = mid + 1
            else:  # i <= new_items[mid]
                r = mid

        print(f"  Inserting at position {l}")
        new_items.insert(l, i)
    return new_items

main()
