from django.test import TestCase
from django.utils.html import escape
from django.http import HttpRequest
from lists.views import home_page
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from unittest import skip


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text': 'A new item for an existing list'})

    def tests_redirects_to_list_view(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % correct_list.id,
            data={'text': 'A new item for an existing list'})

        self.assertRedirects(response, '/lists/%d/' % correct_list.id)


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual('A new list item', new_item.text)

    def test_redirects_after_a_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % new_list.id)

    def test_invalid_list_items_arent_created(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEquals(List.objects.count(), 0)
        self.assertEquals(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/%d/' % list_.id, data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % correct_list.id)
        self.assertEqual(response.context['list'], correct_list)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemy 1', list=correct_list)
        Item.objects.create(text='itemy 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % correct_list.id)

        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % list_.id)
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    @skip
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemy', list=list_)
        response = self.client.post(
            '/lists/%d/' % list_.id,
            data={'text': 'itemy'})
        expected_error = escape("You've already got this in your list")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        self.assertContains(response, expected_error)
        self.assertEqual(Item.objects.all().count(), 1)


class HomePageTest(TestCase):
    maxDiff = None

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemy 1', list=list_)
        Item.objects.create(text='itemy 2', list=list_)

        response = self.client.get('/lists/%d/' % list_.id)

        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertTemplateUsed('home.html')
