<%inherit file="layout.mako"/>

<div class="content">
  <h1>
    All of books:
  </h1>
  <h2>
    % for book in books:
        ${book.name}${'.' if loop.last else ','}\
    % endfor
  </h2>
</div>
