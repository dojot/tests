class Utils {
    static sid() {
        return (1 + Math.random() * 429496729125).toFixed().toString();
    }

    static toString(value) {
        let valueToShow = 'undefined';
        if (((typeof value) === 'boolean')) {
            valueToShow = (value ? 'true' : 'false');
        } else if ((typeof value) === 'number' || (typeof value) === 'string') {
            valueToShow = value.toString();
        }
        return valueToShow;
    }

    static randomString() {
        return Math.random()
            .toString(36)
            .substring(2, 15)
            + Math.random()
                .toString(36)
                .substring(2, 15);
    }

    static uppercaseFirstLetter(string) {
        return string.charAt(0)
            .toUpperCase() + string.slice(1);
    }
}

module.exports = Utils;
