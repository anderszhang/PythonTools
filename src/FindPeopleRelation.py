'''
Created on 2011-10-31
�����������Ĺ�ϵ
@author: anderszhang
@mail:zhangzhang@gmail.com
'''

relation =[]
def findRelation(startPoint,endPoint):
    friends = findFriends(startPoint);
    for friend in friends:
        if(friend!=endPoint):
            relation.append(friend)

#����ĳ�˵ĺ���
def findFriends(startPoint):
    friends =[]
    return friends