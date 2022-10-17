% if not request.is_authenticated:
<a href="${ request.route_url('login') }">Login</a>
</p<p class="pull-right">
    % else:
<form class="pull-right" action="${ request.route_url('logout') }" method="post">
    ${request.identity.initials}
    <input type="hidden" name="csrf_token" value="${ get_csrf_token() }">
    <button class="btn btn-link" type="submit">Logout</button>
</form>
% endif
${self.body()}
