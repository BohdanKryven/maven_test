<%inherit file="layout.mako"/>

<p>
    Editing <strong>${book_name}</strong>
</p>

<form action="${url}" method="post">
    <input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
    <div class="form-group">
        <textarea class="form-control" name="description" rows="10" cols="60">${ description }</textarea>
    </div>
    <div class="form-group">
        <button type="submit" class="btn btn-default">Save</button>
    </div>
</form>