document.addEventListener('DOMContentLoaded', function() {
    
	// Create event handler for the edit button 
    document.querySelectorAll('.edit_button').forEach(function(button) {
        button.onclick = function() {
        	// get id of the post to edit 
        	const post_id = button.dataset.id;
        	// get element to edit 
            document.querySelector(`.content_${post_id}`).style.display = "none";
            // hide button edit
            button.style.display = "none";
            // display edit box
            document.querySelector(`.edit_content_${post_id}`).style.display = "block";
        }
    });

    // Create event handler for the button to post edited content
    document.querySelectorAll('.post_edited_content').forEach(function(button) {
        button.onclick = function() {
        	// get id of the edited post 
        	const post_id = button.dataset.id;
        	// get csrf token
        	const csrftoken = getCookie('csrftoken');
        	// get text from editbox
        	edited_content = document.querySelector(`#edit_content_textarea_${post_id}`).value
        	// fetch to post edited content
            fetch(`/edit_content/${post_id}`, {
			    method: 'POST',
			    headers: {
					'X-CSRFToken': csrftoken,
				},
    			body: JSON.stringify({
          			content: edited_content
				})
			})
            // replace the original post by the edited post 
			document.querySelector(`.content_${post_id}`).innerHTML = edited_content;
			// hide edit box
			document.querySelector(`.edit_content_${post_id}`).style.display = "none";
			// display post box
			document.querySelector(`.content_${post_id}`).style.display = "block";
			// display edit button 
			document.querySelectorAll('.edit_button').forEach(function(button) {
       		button.style.display = "block";
    		});

		};
	});

    // Create event handler for the like button 
	document.querySelectorAll('.like_button').forEach(function(button) {
	    button.onclick = function() {
	    	// get if of the liked post
	    	const post_id = button.dataset.id;
	    	// get csrf token
	    	const csrftoken = getCookie('csrftoken');
	    	// fetch like 
	        fetch(`/like_post/${post_id}`,
			    {
				method: "POST",
				headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken,
				}
			}).then(response => response.json())
  			.then(data => {
  				// if post is liked 
  				if (data == "liked"){
  					// get like_count to update in DOM 
  					var like_count = document.querySelector(`#like_counter_${post_id}`).innerHTML;
  					// update count 
	        		like_count = parseInt(like_count)+1;
	        		// diplay updated count 
					document.querySelector(`#like_counter_${post_id}`).innerHTML = like_count;
					// change button in DOM
					button.innerHTML = '<svg height="18" viewBox="0 -20 464 464" xmlns="http://www.w3.org/2000/svg"><path d="m340 0c-44.773438.00390625-86.066406 24.164062-108 63.199219-21.933594-39.035157-63.226562-63.19531275-108-63.199219-68.480469 0-124 63.519531-124 132 0 172 232 292 232 292s232-120 232-292c0-68.480469-55.519531-132-124-132zm0 0" fill="#ff6243"/><path d="m32 132c0-63.359375 47.550781-122.359375 108.894531-130.847656-5.597656-.769532-11.242187-1.15625025-16.894531-1.152344-68.480469 0-124 63.519531-124 132 0 172 232 292 232 292s6-3.113281 16-8.992188c-52.414062-30.824218-216-138.558593-216-283.007812zm0 0" fill="#ff5023"/>Like</svg>'
					}
				// if post is unliked 	
				else{
					// get like_count to update in DOM
					var like_count = document.querySelector(`#like_counter_${post_id}`).innerHTML;
					// update count 
	        		like_count = parseInt(like_count)-1;
	        		// diplay updated count 
					document.querySelector(`#like_counter_${post_id}`).innerHTML = like_count;
					// change button in DOM
					button.innerHTML = '<svg height="18" viewBox="0 -20 480 480" xmlns="http://www.w3.org/2000/svg"><path d="m348 0c-43 .0664062-83.28125 21.039062-108 56.222656-24.71875-35.183594-65-56.1562498-108-56.222656-70.320312 0-132 65.425781-132 140 0 72.679688 41.039062 147.535156 118.6875 216.480469 35.976562 31.882812 75.441406 59.597656 117.640625 82.625 2.304687 1.1875 5.039063 1.1875 7.34375 0 42.183594-23.027344 81.636719-50.746094 117.601563-82.625 77.6875-68.945313 118.726562-143.800781 118.726562-216.480469 0-74.574219-61.679688-140-132-140zm-108 422.902344c-29.382812-16.214844-224-129.496094-224-282.902344 0-66.054688 54.199219-124 116-124 41.867188.074219 80.460938 22.660156 101.03125 59.128906 1.539062 2.351563 4.160156 3.765625 6.96875 3.765625s5.429688-1.414062 6.96875-3.765625c20.570312-36.46875 59.164062-59.054687 101.03125-59.128906 61.800781 0 116 57.945312 116 124 0 153.40625-194.617188 266.6875-224 282.902344zm0 0"/>Like</svg>'
				}
  			});
			};
		});
	
	// if it is the profile page 
	if (document.body.contains(document.getElementById("follow_button")))
	{
		// create event handler for follow button
		document.getElementById("follow_button").addEventListener('click', () => 
		{
			// get followed user id 
			const user_id = document.getElementById("follow_button").getAttribute('data-user');
			// get csrf token 
	    	const csrftoken = getCookie('csrftoken');
	    	// fetch follow
			fetch(`/follow_user/${user_id}`,
			    {
				method: "POST",
				headers: {
				'Accept': 'application/json',
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken,
				}
			}).then(response => response.json())
  			.then(data => {
  				// if user is followed
  				if (data == "followed"){
  					// get follower count to update in DOM 
  					var followers_count = document.querySelector('#followers_count').innerHTML;
	        		followers_count = parseInt(followers_count)+1;
	        		// update followers count in DOM 
					document.querySelector(`#followers_count`).innerHTML = `${followers_count}: followers`;
					// update in DOM 
					document.querySelector(`#follow_button`).innerHTML = "Unfollow"
				}
				// if user is unfollow 
				else{
					// get follower count to update
  					var followers_count = document.querySelector('#followers_count').innerHTML;
	        		console.log(followers_count);
	        		followers_count = parseInt(followers_count)-1;
	        		// update count and button in DOM 
					document.querySelector(`#followers_count`).innerHTML = `${followers_count}: followers` ;
					document.querySelector(`#follow_button`).innerHTML = "Follow"
				}
			})


		});
	}
});



// get csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}