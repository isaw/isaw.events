AdvancedQuery
=============

``AdvancedQuery`` is a Zope product aimed to overcome several limitations
and bugs of ``ZCatalog``'s native search function.

Like ``ZCatalog`` search, it supports elementary index searches.
While ``ZCatalog`` can combine such elementary searches only by "and",
``AdvancedQuery`` allows to arbitrarily combine them by ``&`` (and),
``|`` (or) and ``~`` (not). Besides, it supports an extended range
of elementary queries, such as matching, indexed queries, literal
result sets. Finally, it supports incremental filtering.

``AdvancedQuery`` also extends the sorting capabilities of
``ZCatalog``. ``ZCatalog`` supports efficient index based sorting
on one level. ``AdavancedQuery`` supports sorting on arbitrary levels
of field indexes. Furthermore, sorting is performed incrementally
-- only as far as the result is accessed.
This can drastically speed up sorting.
Finally, ``AdvancedQuery`` can sort based on query based ranks.
Unlike ``ZCatalog`` which simply ignores hits for which it does not
have a sort value, ``AdvancedQuery`` sorts such hits at the end
of the respective list.

``AdvancedQuery`` works best when used together with
``Products.ManagableIndex`` and ``dm.incrementalsearch``.
Some of its features depend on these products, e.g. matching
and incremental filtering. Furthermore, these additional
components can speed up queries by several orders of magnitude.

For more information, see ``AdvancedQuery.html`` in the ``doc`` subfolder.
