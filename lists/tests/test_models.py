from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(2, saved_items.count())

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertIn('The first (ever) list item', first_saved_item.text)
        self.assertEquals(first_saved_item.list, list_)
        self.assertIn('Item the second', second_saved_item.text)
        self.assertEquals(second_saved_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.full_clean()
            item.save()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEquals(list_.get_absolute_url(), '/lists/%d/' % list_.id)

    def test_cannot_save_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='do thing')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='do thing')
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        Item.objects.create(text='do thing', list=list1)
        list2 = List.objects.create()
        item = Item(list=list2, text='do thing')

        # should not raise
        item.full_clean()

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='i1')
        item2 = Item.objects.create(list=list_, text='item2')
        item3 = Item.objects.create(list=list_, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3])

    def test_string_representation(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='some text')
        self.assertEqual('some text', str(item1))
