document.addEventListener("DOMContentLoaded",()=>{

console.log("OSINT Search Pro iniciado");

document.querySelectorAll(".copy-btn").forEach(btn=>{

btn.addEventListener("click",()=>{

navigator.clipboard.writeText(btn.dataset.url);

btn.innerHTML="✅ Copiado";

setTimeout(()=>{

btn.innerHTML="Copiar URL";

},2000);

});

});

});