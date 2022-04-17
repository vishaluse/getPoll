console.log("hehe boi")

const optionBox = document.getElementById('option-box')
const helloBox = document.getElementById('hello')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')



const url = window.location.href

const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time over')
                sendData()
            }, 500)
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}



$.ajax({
    type: 'GET',
    url: `${url}/data`,
    success: function(response){
        console.log(response)
        const data = response.data
        console.log("I am a gap")
        console.log(response.is_voted)
        if(response.is_voted) {
            for (const [key, value] of Object.entries(data)) {
                hello.innerHTML += `
                        <hr>
                        <div  class="mb-2">
                            <b>${key}</b>
                        </div>
                        <br><div class="ui negative message">
                        <div class="header">
                        You have already voted
                        </div>
                        <p>try other polls or create a new one.
                    </p></div>
                    `
            }
          
        } else {
            for (const [key, value] of Object.entries(data)) {
                optionBox.innerHTML += `
                        
                        <div  class="mb-2">
                            <b>${key}</b>
                        </div>
                    `
                    value.forEach(v=>{
                        optionBox.innerHTML += `
                            <div>
                                <input type="radio" class="ans" id="${key}-${v}" name="${key}" value="${v}">
                                <label for="${key}">${v}</label>
                            </div>
                        `
                    })
              }
              activateTimer(response.time)
        }
        
    },
    error: function(error){
        console.log(error)
    }
})

const optionForm = document.getElementById('option-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')



const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    // console.log(elements)
    data['csrfmiddlewaretoken'] = csrf[0].value
   
    // console.log(data)
    elements.forEach(el=>{
        if(el.checked) {
            data[el.name] = el.value
        } else {
            if(!data[el.name]) {
                data[el.name] = null
            }
        }
    })

    // console.log(data)



    $.ajax({
        type: 'POST',
        url: `${url}/save`,
        data: data,
        success: function(response){
            window.location.href = url;

            console.log(response)
        },
        error: function(error){
            console.log(error)
        }
    })
}

optionForm.addEventListener('submit', e=>{
    e.preventDefault()
    sendData()
})