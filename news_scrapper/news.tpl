%#template to generate a HTML ul from a list of tuples (or list of lists, or tuple of tuples or ...)
<h3>The todays latest news are:</h3>
<ul>
%for row in rows:
   <li><a href='{{ row.url }}'>{{ row.name }}</a></li>
%end
</ul>