from .forms import *
from django.db.models import Q
from .models import *

class Mixins(object):

#Select Mixins
    objectForm_1 = ''
    query_value_list = []
    initial_order = ''
    search_parameters_results_order = []
    objectForm=''

    def get_object_form(self):
        return self.objectForm_1

    def get_query_value_list(self):
        return self.query_value_list

    def get_initial_order(self):
        return self.initial_order

    def get_search_parameters_results_order(self):
        return self.search_parameters_results_order

    def get_primary_key(self):
        return self.initial_order

class MyMixin_Profiles(Mixins):

    objectModel = profiles
    query_value_list = ['profileID','profileIndex_FK__profileIndexTitle','categoryID_FK__categoryTitle','subCategoryID_FK__subCategoryTitle', 'profileIndex_FK', 'categoryID_FK','subCategoryID_FK']
    initial_order = '-profileID'
    search_parameters_results_order = ['profileID','profileIndex_FK__profileIndexTitle','categoryID_FK__categoryTitle','subCategoryID_FK__subCategoryTitle', 'profileIndex_FK', 'categoryID_FK','subCategoryID_FK']
    objectForm=profilesForm

    def get_search_parameters(self, searchF):

        Q1 = Q(profileID__icontains=searchF)
        Q2 = Q(profileIndex_FK__profileIndexTitle__icontains=searchF)
        Q3 = Q(categoryID_FK__categoryTitle__icontains=searchF)
        Q4 = Q(subCategoryID_FK__subCategoryTitle__icontains=searchF)

        args_list = [Q1, Q2, Q3, Q4]
        args = Q()
        for each_args in args_list:
            args = args | each_args
        return args

    def get_delete_ID(self,item_id):
        filter ={'profileID': item_id}
        return filter

    def get_pk_ID(self,item_id):
        filter ={'profileID': item_id}
        return filter

class MyMixin_Categories(Mixins):

    objectModel = category
    query_value_list = ['categoryID', 'categoryTitle']
    initial_order = '-categoryID'
    search_parameters_results_order = ['categoryID','categoryTitle']
    objectForm=categoryForm

    def get_search_parameters(self, searchF):

        Q1 = Q(categoryID__icontains=searchF)
        Q2 = Q(categoryTitle__icontains=searchF)
        args_list = [Q1, Q2]
        args = Q()
        for each_args in args_list:
            args = args | each_args
        return args

    def get_delete_ID(self,item_id):
        filter ={'categoryID': item_id}
        return filter

    def get_pk_ID(self,item_id):
        filter ={'categoryID': item_id}
        return filter


class MyMixin_ProfileIndex(Mixins):

    objectModel = profilesIndex
    query_value_list = ['profileIndex_PK','profileIndexTitle']
    initial_order = '-profileIndex_PK'
    search_parameters_results_order = ['profileIndex_PK','profileIndexTitle']
    objectForm=profilesIndexForm

    def get_search_parameters(self, searchF):

        Q1 = Q(profileIndex_PK__icontains=searchF)
        Q2 = Q(profileIndexTitle__icontains=searchF)

        args_list = [Q1, Q2]
        args = Q()
        for each_args in args_list:
            args = args | each_args
        return args

    def get_delete_ID(self,item_id):
        filter ={'profileIndex_PK': item_id}
        return filter

    def get_pk_ID(self,item_id):
        filter ={'profileIndex_PK': item_id}
        return filter



class MyMixin_Elements(Mixins):

    objectModel = subCategory
    query_value_list = ['subCategoryID', 'subCategoryTitle', 'subCategoryLink','subCategorySort']
    initial_order = '-subCategoryID'
    search_parameters_results_order = ['subCategoryID', 'subCategoryTitle', 'subCategoryLink','subCategorySort']
    objectForm=SubCategoryForm

    def get_search_parameters(self, searchF):

        Q1 = Q(subCategoryID__icontains=searchF)
        Q2 = Q(subCategoryTitle__icontains=searchF)
        Q3 = Q(subCategoryLink__icontains=searchF)
        Q4=  Q(subCategorySort__icontains=searchF)

        args_list = [Q1, Q2,Q3,Q4]
        args = Q()
        for each_args in args_list:
            args = args | each_args
        return args

    def get_delete_ID(self,item_id):
        filter ={'subCategoryID': item_id}
        return filter

    def get_pk_ID(self,item_id):
        filter ={'subCategoryID': item_id}
        return filter



class MyMixin_UserRights(Mixins):

    objectModel = userRights
    query_value_list = ['rightID','userID__username','profilesIndex_FK__profileIndexTitle','profilesIndex_FK','userID']
    initial_order = '-rightID'
    search_parameters_results_order = ['rightID','userID__username','profilesIndex_FK__profileIndexTitle','profilesIndex_FK','userID']
    objectForm=userRightsForm

    def get_search_parameters(self, searchF):

        Q1 = Q(rightID__icontains=searchF)
        Q2 = Q(profilesIndex_FK__profileIndexTitle__icontains=searchF)
        Q3 = Q(userID__username__icontains=searchF)


        args_list = [Q1, Q2,Q3]
        args = Q()
        for each_args in args_list:
            args = args | each_args
        return args

    def get_delete_ID(self,item_id):
        filter ={'rightID': item_id}
        return filter

    def get_pk_ID(self,item_id):
        filter ={'rightID': item_id}
        return filter



