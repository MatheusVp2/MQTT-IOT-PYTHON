const server_host = document.domain
const server_port = document.port

const new_lat  = 0
const new_long = 0

/* Variaveis para atualização e criação do MAPA */
const var_latitude  = document.querySelector('.var_latitude')
const var_longitude = document.querySelector('.var_longitude')

var_latitude.innerHTML  = new_lat
var_longitude.innerHTML = new_long

const mymap = L.map('mapid').setView([new_lat, new_long], 3);
const marker = L.marker([new_lat, new_long]).addTo(mymap);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: "Mapa Projeto PI",
    maxZoom: 500,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoibWF0aGV1c3ZwMiIsImEiOiJja2h3NG0ycWUwNm8xMnB0aGVqZWZsbzd3In0.llNUZ3O9pfjSqfsWcrKRig'
}).addTo(mymap);

/* Função para atualização dos dados do MAPA */
function atualizaMapa(lat, long){
    console.log("[ATT MAP] Atualizando Mapa - Dados MQTT \n")
    mymap.setView([lat, long], 16)
    marker.setLatLng( [lat, long] )
    var_latitude.innerHTML = lat
    var_longitude.innerHTML = long
}

/* Função o click do Botao // Envio padrao de Coordenadas */
function botao_clicado(valor){
    var opx = valor.value

    switch (opx) {
        case 'morro':
            console.log("[ATT MAP] Morro do Moreno ES ( -20.326324, -40.277168 )")
            publishMQTT( -20.326324, -40.277168 )
            // -20.326324, -40.277168
            break;

        case 'convento':
        console.log("[SEND MAP to MQTT] Convento da Penha ES ( -20.329308, -40.287367 )")
        publishMQTT( -20.329308, -40.287367 )
        // -20.329308, -40.287367
            break;
    
        case 'ilha':
        console.log("[SEND MAP to MQTT] Ilha do Boy ES ( -20.309804, -40.281716 )")
        publishMQTT( -20.309804, -40.281716 )
        // -20.309804, -40.281716
            break;
        
        case 'cristo':
        console.log("[SEND MAP to MQTT] Cristo Rendetor RJ ( -22.952018, -43.212119 )")
        publishMQTT( -22.952018, -43.212119 )
        // -22.952018, -43.212119
            break;
    }
}

/**/
async function pegaUltimaCoordInDojot() {
    console.log("[ATT LAST GEO] Atualizando ultima informação de localização do MQTT")
    try {
        var response = await axios.get('/device/a68745/attr/geo');
        var data     = response.data[0].value
        var mqtt_geo = data.split(',')
        atualizaMapa(mqtt_geo[0], mqtt_geo[1])
    } catch (error) {
        console.error(error);
    }
}

pegaUltimaCoordInDojot()

const topic_mqtt_publi = '/admin/a68745/attrs'
const topic_mqtt_subs  = '/admin/a68745/config'
const qos_mqtt         = '0'

var socket = io.connect('http://' + document.domain + ':' + location.port);

subscribeMQTT()

function publishMQTT(lat, lng){
    console.log("[SEND MQTT] Enviado dados ao MQTT")
    var message = `{ "geo" : "${lat},${lng}" }`
    console.log(`[SEND GEO] Enviado => ${message} `)
    var newData = `{ "topic" : "${topic_mqtt_publi}", "message" :  ${message}, "qos" : ${qos_mqtt} }`;
    socket.emit('publish', data=newData);
}

function subscribeMQTT(){
    console.log("[SUBS TOPIC] Topico => " + topic_mqtt_subs)
    var data = '{"topic": "' + topic_mqtt_subs + '", "qos": ' + qos_mqtt + '}';
    socket.emit('subscribe', data=data);
}

function unsubscribeMQTT(){
    socket.emit('unsubscribe_all');
}

function verificaChave(array, chave){
    return ( array.indexOf(chave) > -1 )
}

socket.on('mqtt_message', function(data) {
    console.log(`[DATA MQTT] Recebendo dados MQTT`);

    var retorno = JSON.parse( data.payload )
    var arrayChaves = Object.keys(retorno)
    
    console.log(retorno)

    if( verificaChave(arrayChaves, "geo") ){
        var mqtt_geo = retorno.geo.split(',')
        atualizaMapa(mqtt_geo[0], mqtt_geo[1])
    }else{
        console.log("Informação não necessaria para Atualizar !")
    }

})