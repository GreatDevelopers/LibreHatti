$.fn.csAccordion = function (args) {
        var defaults = {
            // hoverOver: false,
            customCSS: false,
            delay: 5000,
            autoAnimate: false,
            accordionTitle: false,
            pauseOnHover: true,
            backgroundColour: false,
            titleColour: false,
            titleTextColour: false
        };

        var args = $.extend({}, defaults, args);

        //Globals
        var autoplay;
        var ctx = $(this).attr('id');
        var currentSlide = 0;
        var pause = false;

        /*********************************************
			Initialise CS Accordion
			**********************************************/

        if (args.customCSS) {
            $("<link/>", {
                rel: "stylesheet",
                type: "text/css",
                href: customCSS
            }).appendTo("head");
        }

        var $this = this;



        if (args.accordionTitle) {
            $(this).prepend('<div class="csAccordion__title">' + args.accordionTitle + '</div>');
        }

        $(this).find('ul').wrap('<div class="wrapper"></div>');





            $(this).find('li').each(function () {
                var content = $(this).html();

                if (args.highlightFeatured && $(this).data('featured') == true) {
                    $(this).addClass('featured');
                }


                var html = '';
                    html += '<div class="col heading">';
                if ($(this).data('title')) {
                    html += '<p class="h3">' + $(this).data('title') + '</p><div class="expand"></div>';
                }

                    html += '</div><div class="col content"><div class="inner_content">' + content + '</div>';





                $(this).empty().append(html);
            });


        /*********************************************
			Configure CS Ticker
			**********************************************/

        $(this).addClass('csAccordion');


        if(args.backgroundColour){
         $(this).css('background', args.backgroundColour);
        }
        if(args.titleColour){
            $(this).find('.csAccordion__title').css('background', args.titleColour);
        }
        if(args.titleTextColour){
            $(this).find('.csAccordion__title').css('color', args.titleTextColour);
        }


        function setupAnimation($this) {
            setInterval(function () {
                animate($this);
            }, args.delay);
        }

        if(args.pauseOnHover){
            $($this).find('ul').mouseenter(function () {
            	pause = true;
            }).mouseleave(function () {
            	pause = false;
            });
        }

        /*********************************************
			Animation
			**********************************************/

        function animate(context) {
        	if(!pause){
            if (currentSlide < $(context).find('li').length - 1) {

                $(context).find('li:nth-child(' + (currentSlide + 1) + ') .col.heading').click();
              currentSlide++;
            }else {
                currentSlide = 0;
                $(context).find('li:nth-child(' + (currentSlide) + ') .col.heading').click();
            }
         }
     }

        /*********************************************
			Setup Functions
			**********************************************/

        return this.each(function () {
            var $this = $(this);


            $(this).find('li .col.heading').click(function () {
               $($this).find('.collapse').removeClass('collapse');
               $($this).find('li .col.content').removeClass('displayContent').css('height', 0).parent().removeClass('show');
               $(this).parent().addClass('show').find('.col.content').addClass('displayContent').css('height', $(this).parent().find('.inner_content').height());
               $(this).parent().find('.expand').addClass('collapse');
                currentSlide = $(this).parent().index();

            });

            if (args.autoAnimate) {
                setupAnimation($this);
                $($this).find('li:nth-child(1) .col.heading').click();
            }



         $(window).resize(function(){
            $($this).find('.displayContent').css('height', $($this).find('.show').find('.inner_content').outerHeight());
        });

        });
    };

$(document).ready(function()
                  {
                    $('.accordion').csAccordion({ 'accordionTitle': 'Advanced Settings'});
                  });
