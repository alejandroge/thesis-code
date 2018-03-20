import pdb

dict = {
    0: 'UKN',
    1: 'a',
    2: 'b',
    3: 'c',
    4: 'd',
    5: 'e',
    6: 'f',
    7: 'g',
    8: 'h',
    9: 'i',
    10: 'j'
}

sub = [1, 3, 5, 7, 9]

lst = range(10)
print(lst)

y = [ dict[x] for x in lst if x in sub]
print(y)
