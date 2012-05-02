$(function() {
    function gotAssertion(assertion) {
        if (assertion !== null) {
            var $e = $('#id_assertion');
            $e.val(assertion.toString());
            $e.parent().submit();
        }
    }

    $('#browserid').click(function() {
        navigator.id.get(gotAssertion);
        return false;
    });
});
