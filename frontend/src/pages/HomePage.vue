<script setup>
import { useFetch } from "@vueuse/core";
import { computed, ref } from "vue";
import { store } from "../store";
import { useRouter } from "vue-router";
const userName = ref("");
const apiURL = computed(() => "http://localhost:8000/users/" + userName.value);
const router = useRouter()

</script>

<template>
     <input class="input input-bordered" v-model="store.userName" type="text" @keyup.enter="router.push('/chat')" />

</template>