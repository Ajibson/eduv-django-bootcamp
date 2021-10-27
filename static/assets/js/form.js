const new_category = document.querySelector("#new_category")
let category_select = document.querySelector("#category_select")
// new_category.style.display = "none"

// function showmore(){
//     // Get all the element references you'll need just once:
//     var skillList = document.querySelector("#skillList");
//     var newSkill = document.querySelector("#newSkill");
//     var btnAddSkill = document.querySelector("#btn-add");

//     // Do all of your event binding in JavaScript, not with inline HTML event attributes
//     btnAddSkill.addEventListener("click", addSkill);

//     function addSkill(){
//     if(newSkill.value !== ""){
//     // Don't build new HTML by concatenating strings. Create elements and configure them as objects
//     var li = document.createElement("li");
//     li.textContent = newSkill.value;
//     li.setAttribute("class","list-inline-item border rounded bg-secondary text-white")
    
//     // Only use hyperlinks for navigation, not to have something to click on. Any element can be clicked
//     var span = document.createElement("span");
//     span.classList.add("remove");
//     span.textContent = "X";
//     span.addEventListener("click", removeSkill);  
//     li.appendChild(span);  // Add the span to the bullet
//     skillList.appendChild(li); // Add the bullet to the list
//     newSkill.value = "";	
//     }
//     }
                
//     function removeSkill(){
//     // Just remove the closest <li> ancestor to the <span> that got clicked
//     skillList.removeChild(this.closest("li"));
//     }
// }



function showinput(){
    if(category_select.value === "Others"){
        new_category.style.display = "block"
        new_category.setAttribute("name","category")
        category_select.removeAttribute("name")
        
    }
    else{
        new_category.style.display = "none"
        new_category.removeAttribute("name")
        category_select.setAttribute("name", "category")
    }
}


