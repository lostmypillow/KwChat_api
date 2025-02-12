<script setup>
import { useFetch } from "@vueuse/core";
import { store } from "../store";
const { data } = useFetch("http://localhost:8000/users/" + store.userName);
</script>

<template>
  <div class="card bg-neutral text-neutral-content w-96">
    <div class="card-body items-center text-center flex flex-col gap-8">
      <div class="flex flex-row items-center justify-between w-full">
        <h2 class="card-title">Create chat</h2>
        <button class="btn btn-primary">Close</button>
      </div>

      <div class="flex flex-col items-center justify-center gap-6 w-full">
        <div
          v-for="user in JSON.parse(data)"
          :id="user.user_id"
          class="flex flex-row w-full items-center justify-between"
        >
          <span>{{ user.name }}</span>

          <button class="btn btn-primary">chat</button>
        </div>
      </div>
    </div>
  </div>
</template>
