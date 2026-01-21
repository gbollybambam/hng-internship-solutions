from django.db.models import Q

def apply_filters_to_queryset(queryset, filters):
    query = Q()
    
    if 'is_palindrome' in filters:
        try:
            is_p = filters['is_palindrome'].lower() == 'true'
            query &= Q(is_palindrome=is_p)
        except AttributeError:
             pass

    if 'min_length' in filters:
        try:
            query &= Q(length__gte=int(filters['min_length']))
        except ValueError:
             pass 
             
    if 'max_length' in filters:
        try:
            query &= Q(length__lte=int(filters['max_length']))
        except ValueError:
             pass 

    if 'word_count' in filters:
        try:
            query &= Q(word_count=int(filters['word_count']))
        except ValueError:
             pass
             
    if 'contains_character' in filters and len(filters['contains_character']) == 1:
        char = filters['contains_character']
        query &= Q(**{f'character_frequency_map__{char}__gt': 0})
        
    return queryset.filter(query)