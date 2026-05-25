const drawer=document.getElementById('chapterDrawer');
document.getElementById('drawerBtn')?.addEventListener('click',()=>drawer.classList.add('open'));
document.getElementById('closeDrawer')?.addEventListener('click',()=>drawer.classList.remove('open'));

// Frontend plagiarism protection on reading page.
document.addEventListener('contextmenu',e=>e.preventDefault());
document.addEventListener('copy',e=>e.preventDefault());
document.addEventListener('cut',e=>e.preventDefault());
document.addEventListener('keydown',e=>{
  const key=e.key.toLowerCase();
  if((e.ctrlKey||e.metaKey)&&['c','x','s','p','u','a'].includes(key)) e.preventDefault();
});

let lastSaved=0;
function updateProgress(){
  const scrollTop=window.scrollY;
  const docHeight=document.documentElement.scrollHeight-window.innerHeight;
  const progress=docHeight>0?Math.min(100,(scrollTop/docHeight)*100):0;
  document.getElementById('progressBar').style.width=progress+'%';
  if(window.IS_AUTH && progress-lastSaved>=10){
    lastSaved=progress;
    fetch('/reader/progress',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chapter_id:window.CHAPTER_ID,progress})});
  }
}
window.addEventListener('scroll',updateProgress); updateProgress();

let playing=false;
document.getElementById('musicBtn')?.addEventListener('click',()=>{
  const frame=document.getElementById('ytFrame');
  playing=!playing;
  frame.contentWindow?.postMessage(JSON.stringify({event:'command',func:playing?'playVideo':'pauseVideo',args:[]}), '*');
  document.getElementById('musicBtn').innerText=playing?'Pause Music':'Play Music';
});
