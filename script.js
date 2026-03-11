var map = L.map('map').setView([-27.4323, -48.4306], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);


L.marker([-27.445774,-48.403628])
.addTo(map)
.bindPopup("CIA LATINO AMERICANA DE MEDICAMENTOS");

L.marker([-27.432083,-48.458174])
.addTo(map)
.bindPopup("CIA LATINO AMERICANA DE MEDICAMENTOS");

L.marker([-27.430474,-48.458253])
.addTo(map)
.bindPopup("PANVEL FARMÁCIAS");

L.marker([-27.441147,-48.486762])
.addTo(map)
.bindPopup("PANVEL FARMÁCIAS");

L.marker([-27.441833,-48.502049])
.addTo(map)
.bindPopup("PANVEL FARMÁCIAS");

L.marker([-27.421487,-48.434293])
.addTo(map)
.bindPopup("DROGARIA E FARMACIA CATARINENSE");

L.marker([-27.437546,-48.398995])
.addTo(map)
.bindPopup("PAGUE MENOS");

L.marker([-27.439859,-48.485834])
.addTo(map)
.bindPopup("FARMACIA E DROGARIA SONCINI");

L.marker([-27.445269,-48.403145])
.addTo(map)
.bindPopup("FARMACIA VANIN");

L.marker([-27.396725,-48.427085])
.addTo(map)
.bindPopup("FARMACONTI FARMACIA");

window.onscroll = function() {
    mostrarBotao();
};

function mostrarBotao() {
    var btn = document.getElementById("btnTopo");

    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        btn.style.display = "block";
    } else {
        btn.style.display = "none";
    }
}

function voltarTopo() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

var acc = document.getElementsByClassName("accordion");

for (var i = 0; i < acc.length; i++) {

acc[i].addEventListener("click", function() {

this.classList.toggle("active");

var conteudo = this.nextElementSibling;

if (conteudo.style.display === "block") {
conteudo.style.display = "none";
} else {
conteudo.style.display = "block";
}

});

}

document.getElementById("formPesquisa").addEventListener("submit", function(event){

event.preventDefault();

document.getElementById("mensagem").innerText =
"Obrigado por participar da pesquisa!";

this.reset();

});