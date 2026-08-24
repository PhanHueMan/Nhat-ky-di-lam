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
    // Sử dụng đúng thông số cấu hình từ hình ảnh Firebase của bạn
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
    let isTyping = false;

    // 1. TỰ ĐỘNG TẢI DỮ LIỆU VỀ: Lắng nghe mạng và điền vào các ô id trên màn hình
    database.ref('dulieu_nhatky/').on('value', (snapshot) => {
        if (isTyping) return; // Nếu đang gõ thì tạm thời không đè dữ liệu về

        const data = snapshot.val();
        if (data) {
           console.log("Đã cập nhật dữ liệu mới từ đám mây!");
           const inputs = document.querySelectorAll('input, textarea, select');
           inputs.forEach(input => {
               let key = input.id || input.name;
               if(key && data[key] !== undefined) {
                   if (input.type === 'checkbox') {
                       input.checked = data[key];
                   } else {
                       input.value = data[key];
                   }
               }
           });
        }
    });

    // Theo dõi khi người dùng bắt đầu gõ chữ
    document.addEventListener('input', function() {
        isTyping = true;
    });

    // 2. BỘ NÃO TỰ ĐỘNG LƯU: Cứ sau mỗi 2 giây là tự động quét 10 ô nhập liệu quăng lên mạng!
    setInterval(() => {
        if (isTyping) {
            let dataToSave = {};
            const inputs = document.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                let key = input.id || input.name;
                if (key) {
                    dataToSave[key] = input.type === 'checkbox' ? input.checked : input.value;
                }
            });
            
            database.ref('dulieu_nhatky/').update(dataToSave, (error) => {
                if (!error) {
                    isTyping = false; // Lưu thành công
                    console.log("Hệ thống đã tự động lưu dữ liệu lên đám mây!");
                }
            });
        }
    }, 2000); // 2 giây quét 1 lần
}

window.addEventListener('DOMContentLoaded', loadFirebase);
