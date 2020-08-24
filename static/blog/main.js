

  const form = document.getElementById('cmt-form')
  const btn = document.getElementsByClassName('cmt-btn')
  let comments = document.querySelectorAll('#comment')

  let dotted = document.querySelectorAll('.dotted')
  const delete_comment = document.querySelectorAll('.delete_comment')

  let counts = document.querySelectorAll('#count')

  let comment_display = document.querySelectorAll('.comment-display')
  // console.log(dotted)

  // NodeList to Array
  let array = [...dotted]
  console.log(array)

  // console.log(delete_comment)
  // console.log(comment_display)

    for(let i=0; i < comments.length; i++){
        comments[i].addEventListener('keyup', function(){

            if(this.value.trim() == null || this.value.trim() ==""){
                this.nextElementSibling.style.opacity = .6;;
                this.nextElementSibling.disabled=true;   
            }else if(this.value.trim().length>0){
                this.nextElementSibling.style.opacity = 1;
                this.nextElementSibling.disabled=false;
            }
        })
    }

    for(let i=0; i < btn.length; i++){
        btn[i].addEventListener('click', function(e){
        e.preventDefault()
        let url = '/'
        let text = this.previousElementSibling.value   // in for loop it is possible to do texts_inputs[i] to select resp. input
        if(text.length<1){
            return false
        }

        let id = this.value
        let comment_div = this.parentNode.parentNode.previousElementSibling

        let comment_section = comment_div.previousElementSibling

        fetch(url, {
            method: 'POST',
            headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'comment': text, 'id':id})
        })
         .then((response)=>{
            this.previousElementSibling.value = ""
            return response.json()
        })
         .then((data)=>{

        console.log(data)

        // Comments Count
        counts[i].innerHTML = data.count

        // processing response data
        let new_text = data.text.length <= 150? data.text:data.text.slice(0,150)+"..."


        /*-----
          Create URL
        */
        let image_url = "{% url 'user-posts' 'username' %}".replace('username', data.author)
        let author = data.author
       
       //Creating Elements
       let div_comment_display = document.createElement('div')
       div_comment_display.classList.add("comment-display")

       let img = document.createElement('img')
       img.classList.add("rounded-circle")
       img.classList.add("article-img")
       img.src = data.image

       let div_comment = document.createElement('div')
       div_comment.classList.add('comment')

       //Comment header
       let comment_header = document.createElement('div')
       comment_header.classList.add('comment-header')

       let h5_heading = document.createElement('H5')
       let link = document.createElement('a')
       link.classList.add('mr-2')
       link.href = image_url
       link.text = author
       let span = document.createElement('span')
       span.innerHTML = data.date
       h5_heading.appendChild(link)
       comment_header.appendChild(h5_heading)
       comment_header.appendChild(span)

       let div = document.createElement('div')
       div.classList.add('d-flex')
       div.classList.add('flex-rowr')
       div.classList.add('align-items-center')
       let p_text = document.createElement('p')
       p_text.style.flex = '1';
       p_text.innerHTML = new_text
       let dotted_div = document.createElement('div')
       // dotted_div.onclick = xxx;
       dotted_div.classList.add('d-flex')
       dotted_div.classList.add('flex-column')
       dotted_div.classList.add('p-2')
       dotted_div.classList.add('mb-2')
       dotted_div.classList.add('dotted')
       dotted_div.onclick = delete_toggle
       let dot_span = document.createElement('span')
       let dot_span2 = document.createElement('span')
       let dot_span3 = document.createElement('span')
       dot_span.classList.add('dot')
       dot_span2.classList.add('dot')
       dot_span3.classList.add('dot')
       dot_span.innerHTML = '.'
       dot_span2.innerHTML = '.'
       dot_span3.innerHTML = '.'
       dotted_div.appendChild(dot_span)
       dotted_div.appendChild(dot_span2)
       dotted_div.appendChild(dot_span3)
       div.appendChild(p_text)
       div.appendChild(dotted_div)

       let delete_btn = document.createElement('button')


       div_comment.appendChild(comment_header)
       div_comment.appendChild(div)

       div_comment_display.appendChild(img)
       div_comment_display. appendChild(div_comment) 

       // console.log(div_comment_display)
       comment_div.insertBefore(div_comment_display, comment_div.childNodes[0])
       window.location.reload()
       // array.unshift(div_comment_display)
       // console.log(array.indexOf(div_comment_display))

    })
     .catch(error=>console.log(error))

  })
}

    

  // for (let i = 0; i <dotted.length ; i++) {             
  //     dotted[i].addEventListener('click', function(){
  //         if(delete_comment[i].style.display == 'block'){
  //             delete_comment[i].style.display = 'none';
  //         }
  //         else{delete_comment[i].style.display = 'block';}
  //     })
  // }

  for (let i = 0; i <array.length ; i++) {
      array[i].addEventListener('click', delete_toggle)}

  function delete_toggle(){
    index = array.indexOf(this)
    // if (index === -1) {
    //   index = 0
    // }
    console.log(index)
    if(delete_comment[index].style.display == 'block'){
      delete_comment[index].style.display = 'none';
    }
    else{
      delete_comment[index].style.display = 'block';}
  }


  for (let i = 0; i <delete_comment.length ; i++) {
    delete_comment[i].addEventListener('click', function(){
      // let user = "{{request.user}}"
      // let author = "{{}}"
      const id = this.value
      const url = `/delete-comment/`
      console.log(url)
      fetch(url,{
        'method': 'POST',
        'headers':{
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'id':id})

      }).then(resp => {
          return resp.json()
        })
        .then(data=> {
          console.log(data)
          counts[i].innerHTML = data.count
          comment_display[i].parentNode.removeChild(comment_display[i])

        })
        .catch(err=> console.log(err))
    })
  }