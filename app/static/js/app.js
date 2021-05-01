const app = Vue.createApp({
  data() {
    return {};
  },
});

const Home = {
  name: "Home",
  template: `<div class="row cols-2 g-0">
        <div class="col my-auto justify-content-center text-center">
            <div class="d-flex justify-content-center flex-column my-auto">
                <div>
                    <h1>Buy and Sell</h1>
                    <h1>Cars Online</h1>
                </div>                
                <div class="mx-auto">
                    <p> United Auto Sales provides the fastest, easiest and most user friendly way to buy or sell cars online. Find a Great Price on the Vehicle You Want.</p>
                </div>
                <div>
                    <router-link to="/register" class="btn btn-primary btn-large mx-1">Register</router-link>
                    <router-link to="/login" class="btn btn-success btn-large mx-1">Login</router-link>
                </div>
            </div>
        </div>
        <div class="col">
            <img src="/static/img/front-page.jpg" class="img-fluid" />
        </div>
    </div>`,

  data() {
    return {};
  },
};

app.component("app-header", {
  name: "AppHeader",
  template: `
    <nav class="navbar navbar-dark navbar-expand-lg bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">United Auto Sales</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
                <div class="navbar-nav ms-auto">
                    <ul class="navbar-nav mb-2 mb-lg-0">
                        <li class="nav-item">
                            <router-link class="nav-link" to="/register">Register</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/login">Login</router-link>
                        </li>
                    </ul>
                </div>
                
            </div>
        </div>
  </nav>
    `,
});

app.component("app-footer", {
  name: "AppFooter",
  template: `
    <footer>
        <div class="container">
            <p>Copyright &copy; {{ year }} Flask Inc.</p>
        </div>
    </footer>
    `,
  data() {
    return {
      year: new Date().getFullYear(),
    };
  },
});

app.component("upload-form", {
  template: `
    <form @submit.prevent="uploadPhoto" id="uploadForm" name="uploadForm">
        <div class="form-group">
            <textarea class="form-control" placeholder="Enter description" id="description" name="description" form="uploadForm" rows=4 cols=50></textarea>
            <label for="photo"> Select a file for upload:</label>
            <input class="form-control-file" type="file" id="photo" name="photo">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    `,

  data: function () {
    return {
      csrf: token,
    };
  },

  methods: {
    uploadPhoto: function () {
      let UploadForm = document.getElementById("uploadForm");
      let form_data = new FormData(UploadForm);
      fetch("/api/upload", {
        method: "POST",
        body: form_data,
        headers: {
          "X-CSRFToken": token,
        },
        credentials: "same-origin",
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (jsonResponse) {
          console.log(jsonResponse);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
  data: function () {
    return {};
  },
});

const UploadForm = app.component("upload-form");

const Register = {
  name: "Register",
  template: `
    <div class="container d-flex justify-content-center align-items-center vh-100 flex-column">
    <flash-message :messages="message" :theme="theme"></flash-message>
    <div>
        <h1 class="fs-3 fw-bold mb-3">Register New User</h1>
        <div class="card shadow">
            <div class="card-body">
                <form class="needs-validation" id="registerForm" novalidate @submit.prevent="register">
                    <div class="row">
                        <div class="col">
                            <label for="username" class="form-label text-muted fw-bold">Username</label>
                            <input type="email" v-model="registerForm.username" required class="form-control mb-2" id="username" placeholder="">
                        </div>
                        
                        <div class="col">
                            <label for="password" class="form-label text-muted fw-bold">Password</label>
                            <input type="password" v-model="registerForm.password" required class="form-control" id="password">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <label for="fullname" class="form-label text-muted fw-bold">Fullname</label>
                            <input type="text" v-model="registerForm.fullname" required class="form-control mb-2" id="fullname" placeholder="">
                        </div>
                        
                        <div class="col">
                            <label for="email" class="form-label text-muted fw-bold">Email</label>
                            <input type="email" v-model="registerForm.email" required class="form-control" id="email">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <label for="location" class="form-label text-muted fw-bold">Location</label>
                            <input type="text" v-model="registerForm.location" required class="form-control mb-2" id="location"/>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <label for="biography" class="form-label text-muted fw-bold">Biography</label>
                            <textarea v-model="registerForm.biography" required class="form-control mb-2" id="biography"></textarea>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <label for="upload_photo" class="form-label text-muted fw-bold">Upload Photo</label>
                            <input type="file" id="upload_photo" class="form-control" required mb-2 @change="addFile"  />
                        </div>
                    </div>
                    <div class="d-grid mt-4">
                        <button type="submit" class="btn btn-primary btn-block">Login</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

    `,
  data() {
    return {
      registerForm: {
        username: "",
        password: "",
        fullname: "",
        email: "",
        location: "",
        biography: "",
        photo: null,
        
      },
    };
  },
  methods: {
    addFile(event) {
      this.registerForm.photo = event.target.files;
    },
    register() {
        console.log('dope')
    }
  },
};

const Login = {
  name: "Login",
  template: `
    <div class="container d-flex justify-content-center align-items-center vh-100 flex-column">
        <flash-message :messages="message" :theme="theme"></flash-message>
        <div>
            <h1 class="fs-3 fw-bold mb-3">Login to your account</h1>
            <div class="card shadow">
                <div class="card-body">
                    <form class="needs-validation" id="loginForm" novalidate @submit.prevent="login">
                        <label for="email" class="form-label text-muted fw-bold">Username</label>
                        <input type="email" v-model="loginForm.username" required class="form-control mb-2" id="email" placeholder="">
                        <div class="valid-feedback"></div>
                        <label for="password" class="form-label text-muted fw-bold">Password</label>
                        <input type="password" v-model="loginForm.password" required class="form-control" id="password">
                        <div class="d-grid mt-4">
                            <button type="submit" class="btn btn-primary btn-block">Login</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    `,
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
      },
      csrf: token,
      usernameErrorMessage: "",
      passwordErrorMessage: "",
      message: "",
      theme: "",
    };
  },
  methods: {
    login() {
      const self = this;
      fetch("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(this.loginForm),
        headers: {
          "X-CSRFToken": this.csrf,
          "Content-Type": "application/json",
        },
        credentials: "same-origin",
      })
        .then((response) => {
          return response.json();
        })
        .then((jsonResponse) => {
          console.log(jsonResponse);
          self.message = [jsonResponse.errors.message];
          self.theme = "alert-danger";
        })
        .catch((error) => {
          console.log(error.errors.errors);
          self.message = error.errors;
        });
    },
  },
};

const NotFound = {
  name: "NotFound",
  template: `
    <div>
        <h1>404 - Not Found</h1>
    </div>
    `,
  data() {
    return {};
  },
};

const Alert = app.component("flash-message", {
  template: `
      <div :class='theme' class='alert text-center' role='alert'>
      <ul class="list-unstyled" v-for="message in messages">
        <li v-for="m in message">{{m}}</li>
      </ul>
      </div>
    `,
  props: { messages: Array, theme: String },
  methods: {
    hideAlert() {
      const self = this;
      self.$emit("update:message", "");
    },
  },
  data: function () {
    return {};
  },
  watch: {
    message(newValue) {
      if (newValue) {
        setTimeout(self.hideAlert, 5000);
      }
    },
  },
});

const routes = [
  { path: "/", component: Home },
  { path: "/upload", component: UploadForm },
  { path: "/:pathMatch(.*)*", name: "not-found", component: NotFound },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
];

const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes,
});

app.use(router);

app.mount("#app");
