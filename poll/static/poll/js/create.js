var current_option = 0

function addImage() {
    var element = document.getElementById('add-image')
    var html = `
    <div class="row mt-4" id="current-option-${current_option}">
        <div class="form-group col-md-6">
            <label >Image </label>
            <input type="file" required class="form-control"  name="images" accept="image/*">
        </div>

        <div class="form-group col-md-3 " style="margin-top:35px;">
            <button type="button"  onclick="removeOption(${current_option})" class="btn btn-danger mt-4" >Remove</button>
        </div>
    </div>
    `

    element.innerHTML += html
    current_option += 1


}

function addOption() {
    var element = document.getElementById('add-option')
    var html = `
    <div class="row mt-4" id="current-option-${current_option}">
        <div class="form-group col-md-5">
            <label >Option </label>
            <input type="text" required class="form-control"  name="options" placeholder="enter text">
        </div>

        <div class="form-group col-md-3 " style="margin-top:35px;">
            <button type="button" onclick="removeOption(${current_option})" class="btn btn-danger mt-4" >Remove</button>
        </div>
    </div>
    `

    element.innerHTML += html
    current_option += 1

}


function removeOption(id) {
    var element = document.getElementById(`current-option-${id}`)
    element.remove()

}


firstCollapseWindow = document.getElementById('first-one')

firstCollapseWindow.addEventListener('click', firstOne, false);

function firstOne() {
    var element = document.getElementById('first-one-body')
    var elementPrevious = document.getElementById('second-one-body')
    elementPrevious.innerHTML = ``
    element.innerHTML = ``
    var html = `
        <div class="row mt-4">
            <div class="form-group col-md-5">
                <label >Option</label>
                <input type="text" required class="form-control"  name="options" placeholder="enter text">
            </div>
        </div>


        <div class="row mt-4">
            <div class="form-group col-md-5">
                <label >Option</label>
                <input type="text" required class="form-control"  name="options" placeholder="enter text">
            </div>

            <div class="form-group col-md-3 " style="margin-top:35px;">
                <button type="button" id="option-box" class="btn btn-success mt-4" >Add options</button>
            </div>
        </div>

        <div class="row" id="add-option"></div>
    `

    element.innerHTML += html

    
    const optionBox = document.getElementById('option-box')
    optionBox.addEventListener ("click", addOption, false);
}

SecondCollapseWindow = document.getElementById('second-one')

SecondCollapseWindow.addEventListener('click', secondOne, false);

function secondOne() {
    var element = document.getElementById('second-one-body')
    var elementPrevious = document.getElementById('first-one-body')
    elementPrevious.innerHTML = ``

    element.innerHTML = ``
    var html = `
        <div class="row mt-4">
            <div class="form-group col-md-6">
                <label >Image</label>
                <input type="file" required class="form-control"  name="images" accept="image/*">
            </div>
        </div>


        <div class="row mt-4">
            <div class="form-group col-md-6">
                <label >Image</label>
                <input type="file" required class="form-control"  name="images" accept="image/*">
            </div>

            <div class="form-group col-md-3 " style="margin-top:35px;">
                <button type="button" id="image-box"  class="btn btn-success mt-4" >Add Image</button>
            </div>
        </div>

        <div class="row" id="add-image"></div>

            `

    element.innerHTML += html

    
    const imageBox = document.getElementById('image-box')
    imageBox.addEventListener ("click", addImage, false);
}

