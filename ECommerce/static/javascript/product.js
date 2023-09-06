// for (var i=0; i<document.querySelectorAll(".product-images img").length;i++){
//     document.querySelectorAll(".product-images img")[i].addEventListener("click", function(){
//         alert("I "+ i +" am clicked!");
//     });
// }
document.querySelectorAll(".product-images img")[0].addEventListener("click", function(){
    document.querySelector(".image-sliders").style.backgroundImage = "url('images/products/product-shirt-product-page-1.jpg')";
})

document.querySelectorAll(".product-images img")[1].addEventListener("click", function(){
    document.querySelector(".image-sliders").style.backgroundImage = "url('images/products/product-shirt-2.jpg')";
})

document.querySelectorAll(".product-images img")[2].addEventListener("click", function(){
    document.querySelector(".image-sliders").style.backgroundImage = "url('images/products/product-shirt-3.jpg')";
})

document.querySelectorAll(".product-images img")[3].addEventListener("click", function(){
    document.querySelector(".image-sliders").style.backgroundImage = "url('images/products/product-shirt-product-page-2.jpg')";
})
