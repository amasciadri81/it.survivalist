#!/usr/bin/python3
import pprint as pprint

def sort_dict_1(): 
    dic = {'a': '5', 'b': '4', 'c': '3', 'd': '2', 'e': '1'}

    print ( "original", dic )
            #original {'a': '5', 'b': '4', 'c': '3', 'd': '2', 'e': '1'}

    print ( "sorted 1", sorted(dic.items()) )
            #sorted 1 [('a', '5'), ('b', '4'), ('c', '3'), ('d', '2'), ('e', '1')]

    print ( "sorted 2", sorted(dic.items(), key=lambda item: item[1]) )
            #sorted 2 [('e', '1'), ('d', '2'), ('c', '3'), ('b', '4'), ('a', '5')]

    print ( "sorted 3", {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])} )
            #sorted 3 {'e': '1', 'd': '2', 'c': '3', 'b': '4', 'a': '5'}


def sort_dict_2():
    dic = { 
            'a': { 'z': '3', 'x': '33' },
            'b': { 'z': '2', 'x': '32' },
            'c': { 'z': '1', 'x': '31' }
            }

    print ( "original", dic )
            #original {'a': {'z': '3', 'x': '33'}, 'b': {'z': '2', 'x': '32'}, 'c': {'z': '1', 'x': '31'}}

    print ( "sorted 1", sorted(dic.items()) )
            #sorted 1 [('a', {'z': '3', 'x': '33'}), ('b', {'z': '2', 'x': '32'}), ('c', {'z': '1', 'x': '31'})]
            
    print ( "sorted 2", sorted(dic.items(), key=lambda item: item[1]['z']) )
            #sorted 2 [('c', {'z': '1', 'x': '31'}), ('b', {'z': '2', 'x': '32'}), ('a', {'z': '3', 'x': '33'})]

    print ( "sorted 3", {k: v for k, v in sorted(dic.items(), key=lambda item: item[1]['x'])} )
            #sorted 3 {'c': {'z': '1', 'x': '31'}, 'b': {'z': '2', 'x': '32'}, 'a': {'z': '3', 'x': '33'}}


if __name__ == "__main__":
    print()
    print ("==== SORT 1 ====================================")
    sort_dict_1()
    print()
    print ("==== SORT 2 ====================================")
    sort_dict_2()

