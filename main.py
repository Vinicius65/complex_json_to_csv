# -*- encode: utf-8 -*-

count_recursive = 0
if __name__ == '__main__':
    import json
    import csv

    with open('result.json', encoding='utf-8') as json_file:
        result = json_file.read()
        dict_file = json.loads(result)

        with open('result.csv', 'w', encoding='utf-8', newline='') as csv_file:
            initial_dict = {}
            initial_list = [initial_dict]
            final_list = []

            def recursive_write(old_list, line, old_key, value):
                new_list = []
                if isinstance(value, dict):
                    for partial_k, new_v in value.items():
                        new_k = old_key + '/' + partial_k
                        new_list = recursive_write(new_list or old_list, line, new_k, new_v)
                elif isinstance(value, list):
                    for new_line in old_list:
                        for new_v in value:
                            if isinstance(new_v, dict) or isinstance(new_v, list):
                                new_list.append(new_line)
                                new_list = recursive_write(new_list or old_list, new_line, old_key, new_v)
                            else:
                                copy_dict = new_line.copy()
                                copy_dict[old_key] = new_v
                                new_list.append(copy_dict)
                else:
                    line[old_key] = value
                return new_list or old_list

            for k, v in dict_file.items():
                final_list = recursive_write(final_list or initial_list, initial_dict, k, v)

            csv_write = csv.DictWriter(csv_file, fieldnames=final_list[0].keys(), delimiter=';')
            csv_write.writeheader()
            csv_write.writerows(final_list)

