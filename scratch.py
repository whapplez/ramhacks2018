# infer - no date specified

    # next = ['next', 'this', 'coming']
    # ss = text[dayIndex-3:dayIndex+3]
    # if any(n in ss for n in next):

    # else:
    #     print("Error: Can't infer date")
    #     pass


# location

# ss = ne[dayIndex - 10:dayIndex + 10]
for each in ne:  # ss
    if str(type(each)) == "<class 'nltk.tree.Tree'>":
        typ = each.pos()[0][-1]
        if typ == 'ORGANIZATION' or typ == 'LOCATION':
            location = " ".join([tp[0] for tp in each.leaves()])