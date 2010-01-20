jq(function() {
    var dest = jq('dl.toc dd.portletItem');
    var content = getContentArea();
    if (!content || !dest.length) return;
    
    dest.empty();

    var location = window.location.href;
    if (window.location.hash)
        location = location.substring(0, location.lastIndexOf(window.location.hash));

    var stack = [];
    // Get headers in document order
    jq(content).find('*').filter(function() { return /^h[1234]$/.test(this.tagName.toLowerCase()) })
              .not('.documentFirstHeading').each(function(i) {
        var level = this.nodeName.charAt(1) - 1;
        // size the stack to the current level
        while (stack.length < level) {
            var ol = jq('<ol>');
            if (stack.length) {
                var li = jq(stack[stack.length - 1]).children('li:last');
                if (!li.length)
                    // create a blank li for cases where, e.g., we have a subheading before any headings
                    li = jq('<li>').appendTo(jq(stack[stack.length - 1]));
                li.append(ol);
            }
            stack.push(ol);
        }
        while (stack.length > level) stack.pop();
        
        jq(this).before(jq('<a name="section-' + i + '" />'));

        jq('<li>').append(
            jq('<a />').attr('href', location + '#section-' + i)
                    .text(jq(this).text()))
            .appendTo(jq(stack[stack.length - 1]));
    });

    if (stack.length) {
        jq('dl.toc').show();
        oltoc = jq(stack[0]);
        numdigits = oltoc.children().length.toString().length;
        //Use a clever class name to add margin that's MUCH easier to customize
        oltoc.addClass("TOC"+numdigits+"Digit");
        dest.append(oltoc);
        
        //scroll to element now.
        var $target = jq(window.location.hash);
        $target = $target.length && $target
	          || jq('[name=' + window.location.hash.slice(1) +']');
	    var targetOffset = $target.offset().top;
	    jq('html,body').animate({scrollTop: targetOffset}, 0);
    }
});
