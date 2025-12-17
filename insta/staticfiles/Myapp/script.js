// Hamburger menu
const toggle = document.getElementById("menu-toggle");
const menu = document.querySelector(".menu-bar");
toggle?.addEventListener("click", ()=> menu.classList.toggle("show"));

// Create post overlay
function openForm(){ document.getElementById("overlay").style.display="flex"; }
function closeForm(){ document.getElementById("overlay").style.display="none"; }
function validatePostForm(){
  const imageInput = document.getElementById("post-image-input");
  if(!imageInput.value){ alert("Please select an image."); return false; }
  return true;
}

// Comment toggle
document.querySelectorAll(".toggle-comment").forEach((btn,i)=>{
  btn.addEventListener("click",()=> {
    const container = document.querySelectorAll(".comment-container")[i];
    container.style.display = container.style.display==="block"?"none":"block";
  });
});

// Like animation
document.querySelectorAll(".post-image-img").forEach((img, i)=>{
  img.addEventListener("dblclick",()=>{
    const anim = document.getElementById(`like-anim-${i+1}`);
    anim.classList.add("show");
    setTimeout(()=>anim.classList.remove("show"),700);
  });
});
