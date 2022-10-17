<%inherit file="layout.mako"/>

<div class="content">
    <h1>
        Title: ${book.name}
    </h1>
    <h2>
        About: ${book.description}
    </h2>
    <h3>
        Author: ${book.author.initials}
    </h3>
</div>
