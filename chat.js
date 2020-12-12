let websocket = null, connection = null
       function log(msg) {
         const control = globalThis.document.querySelector('div')
         control.innerHTML = control.innerHTML + new globalThis.Date + msg + '<br>'
         //control.scrollTop(control.scrollTop() + 1000)
       }

const stream = await globalThis.navigator.mediaDevices.getUserMedia({video:true, audio:true})
globalThis.document.querySelector('video').srcObject = stream
connection = new globalThis.RTCPeerConnection()
for (const _ of stream.getTracks()) connection.addTrack(_, stream)
connection.ontrack = ({streams}) => globalThis.document.querySelector('video:last-of-type').srcObject = streams[0] 

globalThis.document.querySelector('button').onclick = () =>
{   
    if (globalThis.Object.is(websocket, null))
    {
        websocket = new globalThis.WebSocket(globalThis.location.origin.replace('http', 'ws') + '/ws')
        websocket.onopen = () =>
        {
            const name = globalThis.document.querySelector('input')
            websocket.send(name.value)
            log('Connected as ' + name.value)
            name.disabled = true
            globalThis.document.querySelector('button').textContent = 'Disconnect'
            globalThis.document.querySelector('div+input+button').disabled = false
            globalThis.document.querySelector('div+input').disabled = false
            globalThis.document.querySelector('input:last-of-type').disabled = false
            globalThis.document.querySelector('button:last-of-type').disabled = false
        }
        websocket.onmessage = async message =>
        {
            message = globalThis.JSON.parse(message.data)
            if ('join' in message) log('Joined ' + message.name)
            else if ('' in message) log(message.name + ': ' + message[''])
            else if ('disconnect' in message) log('Disconnected ' + message.name)
            else if ('offer' in message)
            {
                connection.setRemoteDescription(new globalThis.RTCSessionDescription(message.offer))
                const answer = await connection.createAnswer()
                connection.setLocalDescription(answer)
                connection.onicecandidate = event =>
                { 
                    if (event.candidate) websocket.send(globalThis.JSON.stringify({candidate:event.candidate, name:message.name}))
                }
                websocket.send(globalThis.JSON.stringify({answer, name:message.name}))
            }
            else if ('answer' in message) connection.setRemoteDescription(new globalThis.RTCSessionDescription(message.answer))
            else if ('candidate' in message) connection.addIceCandidate(new globalThis.RTCIceCandidate(message.candidate))
        }
        websocket.onclose = () =>
        {
            log('Disconnected.')
            websocket = null
            const name = globalThis.document.querySelector('input')
            name.disabled = false
            name.value = ''
            globalThis.document.querySelector('button').textContent = 'Connect'
            globalThis.document.querySelector('div+input+button').disabled = true
            globalThis.document.querySelector('div+input').disabled = true
            globalThis.document.querySelector('input:last-of-type').disabled = true
            globalThis.document.querySelector('button:last-of-type').disabled = true
        }
    }
    else websocket.close()
}
    
globalThis.document.querySelector('div+input+button').onclick = () =>
{
    const text = globalThis.document.querySelector('div+input')
    log(text.value)
    websocket.send(globalThis.JSON.stringify({'':text.value}))
    text.value = ''
    text.focus()
}

globalThis.document.querySelector('button:last-of-type').onclick = async () =>
{
    const offer = await connection.createOffer()
    const name = globalThis.document.querySelector('input:last-of-type').value
    websocket.send(globalThis.JSON.stringify({offer, name}))
    connection.onicecandidate = event =>
    { 
        if (event.candidate) websocket.send(globalThis.JSON.stringify({candidate:event.candidate, name}))
    }
    connection.setLocalDescription(offer)
}
