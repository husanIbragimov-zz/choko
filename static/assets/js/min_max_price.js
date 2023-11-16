// .filter-img {
//     cursor: pointer;
// }

// .filter-wrapper{
//     width: 100%;
//     position: absolute;
//     height: 100vh;
//     width: 100%;
//     background-color: #fff;
// }

// dbn 

$( document ).ready(function() {
    $('#filter-img').click(function(){
        console.log($('#all-filter'))
        $('#all-filter').toggleClass('dbn');
        $('#all-filter').toggleClass('filter-wrapper');
    })

    $('#filter-img-cl').click(function(){
        console.log($('#all-filter'))
        $('#all-filter').toggleClass('dbn');
        $('#all-filter').toggleClass('filter-wrapper');
    })
    // document.querySelector('.filter-img')
});