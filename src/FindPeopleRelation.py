'''
Created on 2011-10-31
查找两人这间的关系
@author: anderszhang
@mail:zhangzhang@gmail.com
'''

relation =[]
def findRelation(startPoint,endPoint):
    friends = findFriends(startPoint);
    for friend in friends:
        if(friend!=endPoint):
            relation.append(friend)

#查找某人的好友
def findFriends(startPoint):
    friends =[]
    return friends