import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class AllQueueViews(BaseMarshallingDomain):

    def __init__(self, queues, lefties, views):
        super(AllQueueViews, self).__init__()
        """An object that represents flow api All Queue Views response object.
           Keyword arguments:
        """
        self.core_views = queues
        self.lefty_views = lefties
        self.zendesk_views = views

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict)
        return ret

    @classmethod
    def _dict_to_obj(cls, all_queue_views):
        all_queue_obj = AllQueueViews(**all_queue_views)

        core_queue_list = [CoreQueueView._dict_to_obj(queue)
                           for queue in all_queue_obj.core_views]
        all_queue_obj.core_views = core_queue_list

        lefty_queue_list = [LeftyQueueView._dict_to_obj(queue)
                            for queue in all_queue_obj.lefty_views]
        all_queue_obj.lefty_views = lefty_queue_list

        zendesk_queue_list = [ZendeskQueueView._dict_to_obj(queue)
                              for queue in all_queue_obj.zendesk_views]
        all_queue_obj.zendesk_views = zendesk_queue_list

        return all_queue_obj


class CoreQueueView(BaseMarshallingDomain):

    def __init__(self, name, tag, source):
        super(CoreQueueView, self).__init__()
        self.name = name.encode('utf8')
        self.tag = tag
        self.source = source

    @classmethod
    def _dict_to_obj(cls, core_queue_dict):
        core_queue_obj = CoreQueueView(**core_queue_dict)
        return core_queue_obj


class LeftyQueueView(BaseMarshallingDomain):

    def __init__(self, name, queue_id, sort):
        super(LeftyQueueView, self).__init__()
        self.name = name.encode('utf8')
        self.queue_id = queue_id
        self.sort = sort

    @classmethod
    def _dict_to_obj(cls, lefty_queue_dict):
        lefty_queue_obj = LeftyQueueView(**lefty_queue_dict)
        return lefty_queue_obj


class ZendeskQueueView(BaseMarshallingDomain):

    def __init__(self, group_id, name):
        super(ZendeskQueueView, self).__init__()
        self.name = name.encode('utf8')
        self.group_id = group_id

    @classmethod
    def _dict_to_obj(cls, zendesk_queue_dict):
        zendesk_queues_obj = ZendeskQueueView(**zendesk_queue_dict)
        return zendesk_queues_obj
