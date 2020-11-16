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

            def control_recursive():
                global count_recursive
                count_recursive += 1
                print(count_recursive)

            def create_new_list(tmp_list, value):
                control_iterator = len(value)
                new_list = []
                for n in range(0, control_iterator):
                    for item in tmp_list:
                        new_list.append(item.copy())
                return new_list

            def test_type_and_call_recursive(item, key, value, old_list):
                new_list = []
                if isinstance(value, dict):
                    new_list = recursive_write(key, value, new_list or old_list)
                elif isinstance(value, list):
                    new_list = create_new_list(new_list or old_list, value)
                    new_list = recursive_write(key, value, new_list or old_list)
                else:
                    if new_list:
                        for new_line in new_list:
                            new_line[key] = value
                    else:
                        item[key] = value
                return new_list or old_list

            def recursive_write(old_key, value_dict_or_list, old_list_lines):
                control_recursive()
                new_list_line = []
                for line in old_list_lines:
                    if isinstance(value_dict_or_list, dict):
                        for new_k, value in value_dict_or_list.items():
                            part_k = old_key + '/' + new_k
                            new_list_line = test_type_and_call_recursive(line, part_k, value, new_list_line or old_list_lines)

                    if isinstance(value_dict_or_list, list):
                        for value in value_dict_or_list:
                            new_list_line = test_type_and_call_recursive(line, old_key, value, new_list_line or old_list_lines)

                return new_list_line or old_list_lines

            for k, v in dict_file.items():
                final_list = recursive_write(k, v, final_list or initial_dict)

            csv_write = csv.DictWriter(csv_file, fieldnames=final_list[0].keys(), delimiter=';')
            csv_write.writeheader()
            csv_write.writerows(final_list)

