from app.invoices import iter_invoices, list_invoices


def test_a_listing_says_how_many_invoices_and_pages_it_has(make_store):
    page = list_invoices(make_store(30), page=1, per_page=10)
    assert (page.total, page.pages, page.per_page) == (30, 3, 10)
    assert len(page.items) == 10


def test_the_second_page_does_not_repeat_the_first(make_store):
    store = make_store(30)
    first = {i.number for i in list_invoices(store, page=1, per_page=10).items}
    second = {i.number for i in list_invoices(store, page=2, per_page=10).items}
    assert len(second) == 10
    assert first.isdisjoint(second)


def test_a_page_size_above_the_limit_is_cut_back(make_store):
    page = list_invoices(make_store(5), per_page=1000)
    assert page.per_page == 100
    assert len(page.items) == 5


def test_an_empty_book_has_one_empty_page(make_store):
    page = list_invoices(make_store(0))
    assert (page.total, page.pages, page.items) == (0, 1, [])


def test_iterating_a_short_book_yields_every_invoice_once(make_store):
    numbers = [i.number for i in iter_invoices(make_store(14), per_page=10)]
    assert len(numbers) == 14
    assert len(set(numbers)) == 14
