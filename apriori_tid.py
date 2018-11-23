import sys

from collections import defaultdict
from optparse import OptionParserf
from itertools import chain, combinations



def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

def joinSet(itemSet, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def get_item_trans_list(data_iterator):
    trans_list = list()
    itemSet = set()
    for record in data_iterator:
        transac = frozenset(record)
        trans_list.append(transac)
        for item in transac:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, trans_list


def itemsetsWithMinsupport(itemSet, trans_list, minSupport, freq_set):
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = set()
        local_set = defaultdict(int)

        for item in itemSet:
                for transac in trans_list:
                        if item.issubset(transac):
                                freq_set[item] += 1
                                local_set[item] += 1

        for item, count in local_set.items():
                support = float(count)/len(trans_list)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet



def run_apriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, trans_list = get_item_trans_list(data_iter)
    #print(data_iter)

    freq_set = defaultdict(int)
    lar_set = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = itemsetsWithMinsupport(itemSet,
                                        trans_list,
                                        minSupport,
                                        freq_set)

    cur_lset = oneCSet
    k = 2
    while(cur_lset != set([])):
        lar_set[k-1] = cur_lset
        cur_lset = joinSet(cur_lset, k)
        cur_cset = itemsetsWithMinsupport(cur_lset,
                                                trans_list,
                                                minSupport,
                                                freq_set)
        cur_lset = cur_cset
        k = k + 1

    def get_support(item):
            """local function which Returns the support of an item"""
            return float(freq_set[item])/len(trans_list)

    toRetItems = []
    #print(lar_set.items)
    #print(len(lar_set))
    for key, value in lar_set.items():
        #print(key,value)
        toRetItems.extend([(tuple(item), get_support(item))
                           for item in value])

    toRetRules = []
    for key, value in lar_set.items()[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            print(_subsets)
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = get_support(item)/get_support(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    for item, support in sorted(items, key=lambda (item, support): support):
        print "item: %s , %.4f" % (str(item), support)
    print "\nRULES---:"
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        print "Rule: %s ==> %s , %.4f" % (str(pre), str(post), confidence)


def dataFromFile(fname):
        """Function which reads from the file and yields a generator"""
        file_iter = open(fname, 'rU')
        for line in file_iter:
                line = line.strip().rstrip(',')                         # Remove trailing comma
                record = frozenset(line.split(','))
                yield record  # yeild is used for generators
        


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default="myfile.txt")
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.005,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.001,
                         type='float')



    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
            inFile = sys.stdin
    elif options.input is not None:
            inFile = dataFromFile(options.input)
    else:
            print 'No dataset filename specified, system with exit\n'
            sys.exit('System will exit')

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = run_apriori(inFile, minSupport, minConfidence)



    printResults(items, rules)
