<template>
  <v-navigation-drawer permanent>
    <v-list>
      <v-list-item
        v-for="item in items"
        :key="item.title"
        :title="item.title"
        link
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
/**
 * @typedef {Object} NavItem
 * @property {string} title
 */

/** @type {NavItem[]} */
const items = [{ title: 'Home' }, { title: 'Settings' }]
</script>
