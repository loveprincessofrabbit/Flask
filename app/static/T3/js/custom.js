jQuery(document).ready(function() {
    "use strict";


    /* ===================================
		PRELOADER
	====================================== */
	// makes sure the whole site is loaded
	jQuery(window).load(function() {
	        // will first fade out the loading animation
	    jQuery(".status").fadeOut();
	        // will fade out the whole DIV that covers the website.
	    jQuery(".preloader").delay(1000).fadeOut("slow");
	});

	/* ===================================
		WOW JS
	====================================== */
	var wow = new WOW(
	  {
	    boxClass:     'wow',      // animated element css class (default is wow)
	    animateClass: 'animated', // animation css class (default is animated)
	    offset:       250,          // distance to the element when triggering the animation (default is 0)
	    mobile:       true,       // trigger animations on mobile devices (default is true)
	    live:         true,       // act on asynchronously loaded content (default is true)
	    callback:     function(box) {
	      // the callback is fired every time an animation is started
	      // the argument that is passed in is the DOM node being animated
	    }
	  }
	);
	wow.init();

	
	/* ===================================
		FEATURED WORKS
	====================================== */
	$('.puge-featured-work-img').magnificPopup({
	  type: 'image',
	  gallery:{
	    enabled:true
	  }
	});


	
	/* ===================================
		ISOTOPE
	====================================== */
	  var $container = $('.puge-portfolio-items');

	  // filter items on button click
	   $container.isotope({
	          filter: '*',
	          itemSelector: '.item',
	          animationOptions: {
	              duration: 750,
	              easing: 'linear',
	              queue: false
	          }
	      });


	  $('#puge-portfolio-filter ul li a').on('click',function(){
	      var selector = $(this).attr('data-filter');
	      $container.isotope({
	          filter: selector,
	          animationOptions: {
	              duration: 750,
	              easing: 'linear',
	              queue: false
	          }
	      });
	    return false;
	  });

	  var $optionSets = $('#puge-portfolio-filter ul'),
	         $optionLinks = $optionSets.find('a');

	         $optionLinks.on('click',function(){
	            var $this = $(this);
	        // don't proceed if already selected
	        if ( $this.hasClass('selected') ) {
	            return false;
	        }
	     var $optionSet = $this.parents('#puge-portfolio-filter ul');
	     $optionSet.find('.selected').removeClass('selected');
	     $this.addClass('selected');
	  });


});
