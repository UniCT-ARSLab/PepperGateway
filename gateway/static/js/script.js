try {
    var subscribe_button = document.querySelector(".subscribe_button");
  } catch (e) {
    if (e instanceof TypeError) {
      console.log("Type Error");
    }
}

subscribe_button.addEventListener('click', function(){
	var subscribing = document.querySelector(".subscribing");
	var thanks = document.querySelector(".thanks");
	var login = document.querySelector(".login");

	subscribing.classList.add("subscribing_active");
	subscribe_button.classList.add("subscribe_button_active");
	setTimeout(function(){
		login.classList.add("login_active");
	}, 1200);
	setTimeout(function(){
		thanks.classList.add("thanks_active");
	}, 1400);

	setTimeout(function(){
		thanks.classList.remove("thanks_active");
		login.classList.remove("login_active");
		subscribing.classList.remove("subscribing_active");
		subscribe_button.classList.remove("subscribe_button_active");
	}, 4000);
});
