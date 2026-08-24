function loadFirebase() {
    var script1 = document.createElement('script');
    script1.src = "https://gstatic.com";
    var script2 = document.createElement('script');
    script2.src = "https://gstatic.com";
    
    script1.onload = function() {
        document.head.appendChild(script2);
    };
    script2.onload = function() {
        startSync();
    };
    document.head.appendChild(script1);
}

function startSync() {
    const firebaseConfig = {
        apiKey: "AIzaSyD8zsFJMsqNpCu491-GAzByQ8dqTZBqHew",
        authDomain: "://firebaseapp.com",
        databaseURL: "https://firebaseio.com",
        projectId: "nhat-ky-di-lam",
        storageBucket: "nhat-ky-di-lam.firebasestorage.app",
        messagingSenderId: "123680164523",
        appId: "1:123680164523:web:be4fcdb5e1118780ae85ee",
        measurementId: "G-GNRPY00TMV"
    };
  
    firebase.initializeApp(firebaseConfig);
    const database = firebase.database();

    // 1. TỰ ĐỘNG ĐỔ DỮ LIỆU VỀ: Lắng nghe mạng và điền vào đúng các ô id của bạn
    database.ref('dulieu_nhatky/').on('value', (snapshot) => {
        const data = snapshot.val();
        if (data) {
           console.log("Đã nhận dữ liệu đồng bộ mới!");
           
           // Tự động tìm tất cả các ô input, textarea, select trên trang web của bạn
           const inputs = document.querySelectorAll('input, textarea, select');
           inputs.forEach(input => {
               let key = input.id || input.name;
               if(key && data[key] !== undefined) {
                   // Điền dữ liệu từ mạng vào màn hình (cho cả đt và máy tính)
                   if (input.type === 'checkbox') {
                       input.checked = data[key];
                   } else {
                       input.value = data[key];
                   }
               }
           });
        }
    });

    // 2. TỰ ĐỘNG GỬI DỮ LIỆU LÊN: Khi bạn gõ chữ hoặc tích chọn ô vuông
    document.addEventListener('change', function(e) {
        if(e.target.matches('input, textarea, select')) {
            let key = e.target.id || e.target.name;
            if(key) {
                let val = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
                database.ref('dulieu_nhatky/' + key).set(val);
            }
        }
    });
}

window.addEventListener('DOMContentLoaded', loadFirebase);
