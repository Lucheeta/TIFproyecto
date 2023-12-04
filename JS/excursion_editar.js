console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
createApp({
data() {
return {
id:0,
nombre:"",
foto:"",
descripcion:0,
url:'http://127.0.0.1:5000/proyectos'+id,
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {

console.log(data)
this.id=data.id
this.nombre = data.nombre;
this.foto=data.foto
this.descripcion=data.descripcion
})
.catch(err => {
console.error(err);
this.error=true
})
},
modificar() {
let proyecto = {
nombre:this.nombre,
foto: this.foto,
descripcion: this.descripcion,
}
var options = {
body: JSON.stringify(proyecto),
method: 'PUT',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro modificado")
window.location.href = "./excursiones.html";
})
.catch(err => {
console.error(err);
alert("Error al Modificar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')