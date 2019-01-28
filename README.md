# py_isolid

isolid is a Python module to work with [Inrupt Solid](https://solid.inrupt.com). It is a simple library for performing basic Solid operations like 


i) getting profile information(Using WebID to get the profile data)

ii) reading public rdf resource data(Using uri to get the public data) 

iii) creating containers/resources,

iv) updating a rdf resource

v) deleting a rdf resource

vi) getting server capabilities etc.,

 
**Pre-requisites:** In order to read and write Solid data, you need your own Solid POD and identity. You can create a POD from [Get a Solid POD](https://solid.inrupt.com/get-a-solid-pod)

## Installation

To install isolid, simply use pip:

```
pip install isolid

```

## Example Usage

i) To get the friends list 

```
    isolid.get_friends_list($WebID) 

```
ii) To get the profile data

```
    isolid.get_solid_profile_data($WebID) 

```

## Useful links

i) [Solid HTTPS REST API Spec](https://github.com/solid/solid-spec/blob/master/api-rest.md)

ii) https://github.com/solid/solid

iii) https://www.w3.org/TR/ldp-primer/