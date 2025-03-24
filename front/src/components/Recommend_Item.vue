<template>
    <div class="container my-5">
        <h1 class="text-center mb-4">Recommendation</h1>
        <div class="card p-4 mb-4">
            <form @submit.prevent="Recommend_Items">
                <div class="mb-3">
                    <input type="text" class="form-control bg-light" v-model="input_object" placeholder="解決したい課題を入力してください" />
                </div>
                <div>
                    <input type="number" class="form-control bg-light" v-model="k" placeholder="類似度上位何位まで表示しますか？" />
                </div>
                <button type="submit" class="btn btn-primary w-100 mt-3">submit</button>
            </form>
        </div>

        <div v-if="isLoading" class="d-flex justify-content-center">
            <div  class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div class="row" v-if="!isLoading && items.length > 0">
            <h1 class="text-center mb-4">Results</h1>
            <div class="col-md-4 mb-4" v-for="(item, index) in items" :key="index">
                <div class="card" style="background-color: #f0f8ff;">
                    <div class="card-body">
                        <h5 class="card-title" style="border-bottom: 1px solid #ccc; padding-bottom: 10px;">PaperID: {{ item.id }}</h5>
                        <p class="card-text">Objective: {{ item.objective }}</p>
                        <p class="card-text">Methods: {{ item.method }}</p>
                        <p class="card-text">Datasets: {{ item.dataset }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="error">
            <p>{{ error }}</p>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
      return {
        input_object: "",
        k: "",
        items: [],
        isLoading: false,
        error: null
      };
  },
  methods: {
      async Recommend_Items() {
        this.error = null;
        this.isLoading = true;
        try {
            const payload = {
                input_object: this.input_object,
                k: this.k
            };
            const response = await axios.post("http://127.0.0.1:8000/recommend/", payload);
            if (response.data.error_message) {
                throw new Error(response.data.error_message);
            }
            this.items = response.data;
        } catch (err) {
            this.error = err.message;
        } finally {
            this.isLoading = false;
        }
      },
  },
};
</script>

<style scoped>

</style>