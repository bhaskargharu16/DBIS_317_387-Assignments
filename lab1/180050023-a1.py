import csv
def preprocess_query(query,flag):
    if query[-1] != ';' and not(flag):
        query += ';'
    before_from = []
    relations = []
    after_where = []
    from_split = query.split("from")
    where_split = query.split("where")
    for token in from_split[0].split()[1:]:
        before_from += [x for x in token.split(',') if x]
    for token in from_split[1].split():
        if token == "where":
            break
        relations.append(token)
    if len(where_split) == 1:
        return before_from,relations,after_where
    where_split = where_split[1].split("=")
    after_where.append(where_split[0].split()[0])
    val = where_split[1]
    val = val.split()
    if len(val) > 1:
        val = " ".join(val)
        after_where.append(val)
    else:
        after_where.append(val[0])
    return before_from,relations,after_where
def query_1a(query):
    _,relations,_ = preprocess_query(query,False)
    if relations[-1] == ';':
        relations = relations[:-1]
        relations[0] += ';'
    with open("csv-files/"+relations[-1][:-1]+".csv") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i!=0:
                print(','.join(row))
            i = i+1
def query_1b(query):
    _,relations,after_where = preprocess_query(query,False)
    a = []
    for x in after_where:
        a += x.split()
    after_where = a
    if after_where[-1] == ';':
        after_where = after_where[:-1]
    if len(after_where) > 2:
        x = " ".join([after_where[-2],after_where[-1]])
        after_where[-2] = x
        after_where = after_where[:-1]
    with open("csv-files/"+relations[-1]+".csv") as f:
        reader = csv.reader(f)
        reader = list(reader)
        column_name = after_where[0]
        column_name_idx = 0
        desired = after_where[-1]
        if after_where[-1][-1] == ";":
            desired = after_where[-1][:-1]
        if not(desired.isdigit()):
            if desired[0] == "'" and desired[-1] == "'":
                desired = desired[1:-1]
        for idx,token in enumerate(reader[0]):
            if token == column_name:
                column_name_idx = idx
        for row in reader[1:]:
            if row[column_name_idx] == desired:
                print(','.join(row))
def query_1c(query):
    before_from,relations,after_where = preprocess_query(query,False)
    for idx,token in enumerate(before_from[:-1]):
        before_from[idx] = token
    a = []
    for x in after_where:
        a += x.split()
    after_where = a
    if after_where[-1] == ';':
        after_where = after_where[:-1]
    if len(after_where) > 2:
        x = " ".join([after_where[-2],after_where[-1]])
        after_where[-2] = x
        after_where = after_where[:-1]
    with open("csv-files/"+relations[-1]+".csv") as f:
        reader = csv.reader(f)
        reader = list(reader)
        column_name = after_where[0]
        column_name_idx = 0
        desired = after_where[-1]
        if after_where[-1][-1] == ";":
            desired = after_where[-1][:-1]
        if not(desired.isdigit()):
            if desired[0] == "'" and desired[-1] == "'":
                desired = desired[1:-1]
        desired_column_ids = []
        for idx,token in enumerate(reader[0]):
            if token == column_name:
                column_name_idx = idx
        for token in before_from:
            for idx,header in enumerate(reader[0]):
                if header == token:
                    desired_column_ids.append(idx)
        for row in reader[1:]:
            if row[column_name_idx] == desired:
                print(','.join([row[i] for i in desired_column_ids]))
def query_2(query):
    _,relations,after_where = preprocess_query(query,False)
    after_where = [x.split()[0] for x in after_where]
    if after_where[-1] == ';':
        after_where = after_where[:-1]
    relations = ''.join([x.split()[0] for x in relations])
    relations = relations.split(',')
    f1  = open("csv-files/"+relations[0]+".csv")
    f2 = open("csv-files/"+relations[-1]+".csv")
    data1 = list(csv.reader(f1))
    data2 = list(csv.reader(f2))
    attribute1 = after_where[0].split('.')[1]
    attribute2 = after_where[-1].split('.')[1]
    if attribute2[-1] == ';':
        attribute2 = attribute2[:-1]
    attribute1_idx = 0
    for idx,token in enumerate(data1[0]):
        if token == attribute1:
            attribute1_idx = idx
    attribute2_idx = 0
    for idx,token in enumerate(data2[0]):
        if token == attribute2:
            attribute2_idx = idx
    for row1 in data1[1:]:
        for row2 in data2[1:]:
            if row1[attribute1_idx] == row2[attribute2_idx]:
                print(','.join(row1 +row2))
def query_3(query):
    _,relations,after_where = preprocess_query(query,False)
    count = 0
    after_where = [x.split()[0] for x in after_where]
    if after_where[-1] == ';':
        after_where = after_where[:-1]
    with open("csv-files/"+relations[-1]+".csv") as f:
        reader = csv.reader(f)
        reader = list(reader)
        column_name = after_where[0]
        column_name_idx = 0
        desired = after_where[-1]
        if after_where[-1][-1] == ";":
            desired = after_where[-1][:-1]
        if not(desired.isdigit()):
            if desired[0] == "'" and desired[-1] == "'":
                desired = desired[1:-1]
        for idx,token in enumerate(reader[0]):
            if token == column_name:
                column_name_idx = idx
        for row in reader[1:]:
            if row[column_name_idx] == desired:
                count = count+1
    print(count)
def preprocess_query4(query,splitter):
    query = query.split(splitter)
    # query_1 = query[0][1:-1]
    query_1 = query[0]
    query_1 = query_1.split("(")[-1].split(")")[0]
    query_2 = query[-1]
    query_2 = query_2.split("(")[-1].split(")")[0]
    # if query_2[-1] == ";":
    #     query_2 = query[-1][1:-2]
    # else:
    #     query_2 = query[-1][1:-1]
    before_from1,relations1,after_where1 = preprocess_query(query_1,True)
    before_from2,relations2,after_where2 = preprocess_query(query_2,True)
    return before_from1,relations1,after_where1,before_from2,relations2,after_where2
def helper(before_from,relations,after_where):
    lst = []
    with open("csv-files/"+relations[-1]+".csv") as f:
        reader = csv.reader(f)
        reader = list(reader)
        selected_col = before_from[0]
        selected_col_idx = 0
        column_name = after_where[0]
        column_name_idx = 0
        desired = after_where[-1]
        if not(desired.isdigit()):
            if desired[0] == "'" and desired[-1] == "'":
                desired = desired[1:-1]
        for idx,token in enumerate(reader[0]):
            if token == column_name:
                column_name_idx = idx
            if token == selected_col:
                selected_col_idx = idx
        for row in reader[1:]:
            if row[column_name_idx] == desired:
                lst.append(row[selected_col_idx])
        return lst
def query_4a(query):
    splitter = "intersect"
    before_from1,relations1,after_where1,before_from2,relations2,after_where2 = preprocess_query4(query,splitter)
    set1 = helper(before_from1,relations1,after_where1)
    set2 = helper(before_from2,relations2,after_where2)
    intersection = list(set(set1) & set(set2))
    print(*intersection,sep='\n')
def query_4b(query):
    splitter = "union"
    before_from1,relations1,after_where1,before_from2,relations2,after_where2 = preprocess_query4(query,splitter)
    set1 = helper(before_from1,relations1,after_where1)
    set2 = helper(before_from2,relations2,after_where2)
    union = list(set(set1) | set(set2))
    print(*union,sep='\n')
def query_parser(query_type,query):
    if query_type == "1a":
        query_1a(query)
    elif query_type == "1b":
        query_1b(query)
    elif query_type == "1c":
        query_1c(query)
    elif query_type == "2":
        query_2(query)
    elif query_type == "3":
        query_3(query)
    elif query_type == "4a":
        query_4a(query)
    elif query_type == "4b":
        query_4b(query)
    return 0
while True:
    query_type = input("Query Type? ")
    if query_type == '0':
        print("exiting...")
        break
    query = input("Enter your query: ")
    query_parser(query_type,query)