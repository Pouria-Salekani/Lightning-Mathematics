

def rearrange_info(info):
    if info['expression_type'] == 'Parametric':
        left, right = info['derivatives'].split(',')
        new_info = {
            'Input': info['expression'],
            'Type': info['expression_type'],
            'Left Derivative': left[6:],
            'Right Derivative': right[8:],
            'Roots': info['roots'],
            'Domain': info['domain'],
            'Range': info['range']
        }
    else:
        new_info = {
            'Input': info['expression'],
            'Type': info['expression_type'],
            'Derivative': info['derivatives'],
            'Roots': info['roots'],
            'Domain': info['domain'],
            'Range': info['range']
        }

    return new_info

