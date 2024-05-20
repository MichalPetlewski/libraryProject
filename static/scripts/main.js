const openingArrow = document.getElementById("opening-arrow");
const userSetting = document.getElementById("user-setting");
const userSettingBefore = document.getElementById("user-sett-before");
const closingArrow = document.getElementById("closing-arrow");


openingArrow.addEventListener("click", function() {
  userSettingBefore.style.visibility = "hidden";
  userSetting.style.visibility = "visible";
  
});

closingArrow.addEventListener("click", function(){
  userSettingBefore.style.visibility = "visible";
  userSetting.style.visibility = "hidden";

});


